package at.fhooe.recyclingserver.client;

import at.fhooe.recyclingserver.model.Product;

import java.util.Optional;

public interface ProductClient {

    Optional<Product> getByCode(String code);
}
