package at.fhooe.recyclingserver.logic;

import at.fhooe.recyclingserver.client.ProductClient;
import at.fhooe.recyclingserver.jpa.ProductRepository;
import at.fhooe.recyclingserver.model.Product;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.Optional;

import static java.util.Objects.requireNonNull;

@Service
public class ProductLogicImpl implements ProductLogic {

    private static final Logger LOG = LoggerFactory.getLogger(ProductLogicImpl.class);
    private final ProductRepository productRepository;
    private final ProductClient productClient;

    public ProductLogicImpl(ProductRepository productRepository, ProductClient productClient) {
        this.productRepository = requireNonNull(productRepository);
        this.productClient = requireNonNull(productClient);
    }

    @Override
    public Optional<Product> getProduct(String code) {
        Optional<Product> productByCode = productRepository.findProductByCode(code);
        if (productByCode.isPresent()) {
            LOG.info("Retrieved Product from DB");
            return productByCode;
        }
        LOG.info("Retrieving Product from OpenFoodFacts");
        return productClient.getByCode(code).map(productRepository::save);
    }
}
