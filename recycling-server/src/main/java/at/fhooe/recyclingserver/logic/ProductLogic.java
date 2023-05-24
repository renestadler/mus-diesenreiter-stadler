package at.fhooe.recyclingserver.logic;

import at.fhooe.recyclingserver.model.Product;

import java.util.Optional;


public interface ProductLogic {
    Optional<Product> getProduct(String code);
}
